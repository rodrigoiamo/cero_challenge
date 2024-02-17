from ceroai_challenge.models.rules import FilterRuleFactory, ContactRuleFactory


class RuleParser:

    @staticmethod
    def parse_rules(json_rules):
        filter_rules = {}
        contact_rules = {}
        for organization_rules in json_rules:
            filter_rules[organization_rules["organization_id"]] = (
                RuleParser.parse_filter_rules(organization_rules["rules"])
            )
            contact_rules[organization_rules["organization_id"]] = (
                RuleParser.parse_contact_rules(organization_rules["rules"])
            )
        return filter_rules, contact_rules

    @staticmethod
    def parse_filter_rules(rules):
        filter_rules = []
        for rule in rules["filter"]:
            filter_rules.append(
                FilterRuleFactory.create_rule(rule["type"], **rule["args"])
            )
        return filter_rules

    @staticmethod
    def parse_contact_rules(rules):
        contact_rules = []
        for rule in rules["contact"]:
            contact_rules.append(
                ContactRuleFactory.create_rule(rule["type"], **rule["args"])
            )
        return contact_rules
