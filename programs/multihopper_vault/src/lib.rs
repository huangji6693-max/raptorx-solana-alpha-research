use anchor_lang::prelude::*;
use anchor_spl::token::{self, Mint, Token, TokenAccount, Transfer};

declare_id!("MHVau1t111111111111111111111111111111111111");

/// Constant denominator for basis points (10,000 bps = 100%).
pub const BPS_DENOMINATOR: u64 = 10_000;
/// Maximum protocol + partner fee cap (100 bps = 1.00%).
pub const MAX_TOTAL_FEE_BPS: u16 = 100;

#[program]
pub mod multihopper_vault {
    use super::*;

    /// Initializes the MultiHopper Revenue-Share & Atomic Route Settlement Vault config.
    pub fn initialize_config(
        ctx: Context<InitializeConfig>,
        protocol_fee_bps: u16,
        partner_share_bps: u16,
    ) -> Result<()> {
        require!(
            protocol_fee_bps <= MAX_TOTAL_FEE_BPS,
            VaultError::FeeExceedsCap
        );
        require!(
            partner_share_bps <= BPS_DENOMINATOR as u16,
            VaultError::InvalidPartnerShare
        );

        let cfg = &mut ctx.accounts.config;
        cfg.authority = ctx.accounts.authority.key();
        cfg.treasury = ctx.accounts.treasury.key();
        cfg.protocol_fee_bps = protocol_fee_bps;
        cfg.partner_share_bps = partner_share_bps;
        cfg.total_qualifying_volume = 0;
        cfg.bump = ctx.bumps.config;
        Ok(())
    }

    /// Executes an atomic route settlement with deterministic partner fee splitting,
    /// strict self-transfer rejection, and minimum output slippage protection.
    pub fn settle_atomic_route(
        ctx: Context<SettleAtomicRoute>,
        principal_amount: u64,
        gross_output_amount: u64,
        min_net_output: u64,
        route_hash: [u8; 32],
    ) -> Result<()> {
        require!(principal_amount > 0, VaultError::ZeroAmount);
        require!(gross_output_amount > 0, VaultError::ZeroAmount);
        require!(
            ctx.accounts.user_source.owner != ctx.accounts.recipient_token.owner
                || ctx.accounts.user_source.mint != ctx.accounts.recipient_token.mint,
            VaultError::CircularSelfTransfer
        );

        let cfg = &mut ctx.accounts.config;
        let total_fee = gross_output_amount
            .checked_mul(cfg.protocol_fee_bps as u64)
            .ok_or(VaultError::MathOverflow)?
            .checked_div(BPS_DENOMINATOR)
            .ok_or(VaultError::MathOverflow)?;

        let partner_fee = total_fee
            .checked_mul(cfg.partner_share_bps as u64)
            .ok_or(VaultError::MathOverflow)?
            .checked_div(BPS_DENOMINATOR)
            .ok_or(VaultError::MathOverflow)?;

        let protocol_fee = total_fee
            .checked_sub(partner_fee)
            .ok_or(VaultError::MathOverflow)?;

        let net_output = gross_output_amount
            .checked_sub(total_fee)
            .ok_or(VaultError::MathOverflow)?;

        require!(net_output >= min_net_output, VaultError::SlippageExceeded);

        // Update cumulative qualifying volume (principal counted once per atomic settlement)
        cfg.total_qualifying_volume = cfg
            .total_qualifying_volume
            .checked_add(principal_amount)
            .ok_or(VaultError::MathOverflow)?;

        let seeds = &[b"vault_config".as_ref(), &[cfg.bump]];
        let signer = &[&seeds[..]];

        // 1. Transfer net output to recipient
        token::transfer(
            CpiContext::new_with_signer(
                ctx.accounts.token_program.to_account_info(),
                Transfer {
                    from: ctx.accounts.vault_token.to_account_info(),
                    to: ctx.accounts.recipient_token.to_account_info(),
                    authority: cfg.to_account_info(),
                },
                signer,
            ),
            net_output,
        )?;

        // 2. Transfer partner revenue share
        if partner_fee > 0 {
            token::transfer(
                CpiContext::new_with_signer(
                    ctx.accounts.token_program.to_account_info(),
                    Transfer {
                        from: ctx.accounts.vault_token.to_account_info(),
                        to: ctx.accounts.partner_token.to_account_info(),
                        authority: cfg.to_account_info(),
                    },
                    signer,
                ),
                partner_fee,
            )?;
        }

        // 3. Transfer protocol fee to treasury
        if protocol_fee > 0 {
            token::transfer(
                CpiContext::new_with_signer(
                    ctx.accounts.token_program.to_account_info(),
                    Transfer {
                        from: ctx.accounts.vault_token.to_account_info(),
                        to: ctx.accounts.treasury_token.to_account_info(),
                        authority: cfg.to_account_info(),
                    },
                    signer,
                ),
                protocol_fee,
            )?;
        }

        emit!(RouteSettledEvent {
            user: ctx.accounts.user.key(),
            partner: ctx.accounts.partner_token.owner,
            principal_amount,
            net_output,
            partner_fee,
            protocol_fee,
            route_hash,
        });

        Ok(())
    }
}

#[derive(Accounts)]
pub struct InitializeConfig<'info> {
    #[account(
        init,
        payer = authority,
        space = 8 + VaultConfig::LEN,
        seeds = [b"vault_config"],
        bump
    )]
    pub config: Account<'info, VaultConfig>,
    #[account(mut)]
    pub authority: Signer<'info>,
    /// CHECK: Verified treasury authority address stored in config
    pub treasury: UncheckedAccount<'info>,
    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct SettleAtomicRoute<'info> {
    #[account(
        mut,
        seeds = [b"vault_config"],
        bump = config.bump
    )]
    pub config: Account<'info, VaultConfig>,
    pub user: Signer<'info>,
    #[account(mut, constraint = user_source.owner == user.key())]
    pub user_source: Account<'info, TokenAccount>,
    #[account(mut, constraint = vault_token.owner == config.key())]
    pub vault_token: Account<'info, TokenAccount>,
    #[account(mut, constraint = recipient_token.mint == vault_token.mint)]
    pub recipient_token: Account<'info, TokenAccount>,
    #[account(mut, constraint = partner_token.mint == vault_token.mint)]
    pub partner_token: Account<'info, TokenAccount>,
    #[account(mut, constraint = treasury_token.mint == vault_token.mint && treasury_token.owner == config.treasury)]
    pub treasury_token: Account<'info, TokenAccount>,
    pub mint: Account<'info, Mint>,
    pub token_program: Program<'info, Token>,
}

#[account]
pub struct VaultConfig {
    pub authority: Pubkey,
    pub treasury: Pubkey,
    pub protocol_fee_bps: u16,
    pub partner_share_bps: u16,
    pub total_qualifying_volume: u64,
    pub bump: u8,
}

impl VaultConfig {
    pub const LEN: usize = 32 + 32 + 2 + 2 + 8 + 1;
}

#[event]
pub struct RouteSettledEvent {
    pub user: Pubkey,
    pub partner: Pubkey,
    pub principal_amount: u64,
    pub net_output: u64,
    pub partner_fee: u64,
    pub protocol_fee: u64,
    pub route_hash: [u8; 32],
}

#[error_code]
pub enum VaultError {
    #[msg("Protocol fee exceeds 100 bps cap")]
    FeeExceedsCap,
    #[msg("Partner share basis points exceed 10,000")]
    InvalidPartnerShare,
    #[msg("Settlement amount must be greater than zero")]
    ZeroAmount,
    #[msg("Circular self-transfer on identical mint is prohibited")]
    CircularSelfTransfer,
    #[msg("Checked arithmetic overflow")]
    MathOverflow,
    #[msg("Net output below user minimum slippage threshold")]
    SlippageExceeded,
}
