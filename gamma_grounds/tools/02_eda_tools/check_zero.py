def check_zero_inflation_by_npu(df, time_block_col='time_block', npu_col='npu_label'):
    """
    Critical check: Are we modeling zeros or actual crime patterns?
    """
    aggregated = df.groupby([npu_col, time_block_col]).size().reset_index(name='count')
    
    total_blocks = len(aggregated)
    zero_blocks = (aggregated['count'] == 0).sum()
    zero_pct = (zero_blocks / total_blocks) * 100
    
    console.print(f"\n[bold]Zero-Inflation Analysis:[/bold]")
    console.print(f"Total NPU × TimeBlock combinations: {total_blocks:,}")
    console.print(f"Blocks with ZERO crimes: {zero_blocks:,} ({zero_pct:.1f}%)")
    
    if zero_pct > 60:
        console.print(Panel(
            "[red]CRITICAL: >60% zeros detected![/red]\n"
            "Standard regression will fail.\n"
            "Use: XGBoost (objective='count:poisson') or statsmodels ZeroInflatedPoisson",
            border_style="red"
        ))
