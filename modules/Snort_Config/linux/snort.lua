---------------------------------------
-- snort3 Configuration file
---------------------------------------

-- Network variables
HOME_NET = 'any'
EXTERNAL_NET = 'any'

-- Rule path
RULE_PATH = './rules/generated'

-- IPS configuration
ips =
{
    rules = RULE_PATH .. '/snort.rules'
}