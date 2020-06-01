class SystemClass:

	INVESTING = 'Investing Banking Core processing system'
	RETAIL = 'Retail customer facing system'
	TRANSACTION = 'Online transaction system'
	FINANCIAL_ANALYSIS = 'Financial Analysis system'

	CORPORATE_ACCOUNTING = 'Corporate Accounting reporting system'
	PAYROLL = 'Payroll system'
	FINANCIAL_REPORTING = 'Financial Internal Reporting system'

	SYSTEM_IMPROVEMENT = 'System improvement requests system'
	CHANGE_MANAGEMENT = 'Change management system'
	TIMESHEET = 'Timesheet hour recording system'

	def __init__(self, name, tier):
		self.name = name
		self.tier = tier

	def to_sql(self):
		return (self.name, self.tier)