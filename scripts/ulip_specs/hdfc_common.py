SFIN = {'Blue Chip Fund': 'ULIF03501/01/10BlueChipFd101', 'Opportunities Fund': 'ULIF03601/01/10OpprtntyFd101', 'Balanced Fund': 'ULIF03901/09/10BalancedFd101',
        'Discontinued Policy Fund': 'ULIF05110/03/11DiscontdPF101', 'Diversified Equity Fund': 'ULIF05501/08/13DivrEqtyFd101', 'Discovery Fund': 'ULIF06618/01/18DiscvryFnd101',
        'Equity Advantage Fund': 'ULIF06723/03/18EqtyAdvtFd101', 'Flexi Cap Fund': 'ULIF07114/07/23FlexiCapFd101', 'India Consumption Advantage Fund': 'ULIF08421/11/25InCnsmAdFd101',
        'Top 500 Smart Value 50 Fund': 'ULIF08801/06/26SmtVal50Fd101', 'Dividend Leaders Advantage Fund': 'ULIF09004/09/26DivLdrAdFd101', 'Top 200 Equal weight Fund': 'ULIF09216/09/26T200EqWtFd101',
        'Bond Fund': 'ULIF05601/08/13BondFunds101', 'Equity Plus Fund': 'ULIF05301/08/13EquityPlus101', 'Liquid Fund': 'ULIF00102/01/04LiquidFund101', 'Bond Plus Fund': 'ULIF06814/06/19BondPlusFd101',
        'Secure Advantage Fund': 'ULIF06914/06/19SecAdvFund101', 'Sustainable Equity Fund': 'ULIF07019/07/21SustnblEqF101', 'Midcap Momentum Fund': 'ULIF07317/01/24MidCpMoIdx101',
        'Nifty Alpha 30 Fund': 'ULIF07528/05/24AlphaIdxFd101', 'Top 500 Momentum 50 Fund': 'ULIF07616/10/24Top500MoFd101', 'Dynamic Advantage Fund': 'ULIF08028/02/25DynamicFnd101',
        'Top 300 Alpha 50 Fund': 'ULIF07828/02/25Alpha300Fd101', 'Top 500 Multifactor 50 Fund': 'ULIF08219/09/25TopMF500Fd101', 'India Sector Leaders Opportunities Fund': 'ULIF08602/03/26InSctrLrFd101'}
def funds(names, fmc=1.35, low=()):
    return [{'name': n, 'SFIN': SFIN.get(n), 'FMC_pct': 0.80 if n in low else fmc, 'asset_allocation': 'see policy document Appendix 2', 'risk_label': None} for n in names]
