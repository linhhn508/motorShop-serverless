# We need to Create the Reusable Delegation Set to
# keep using the same NS server that we added in external domain registar
# aws route53 create-reusable-delegation-set --caller-reference "my-unique-delegation-set-v1"

resource "aws_route53_zone" "linhhn508" {
  name              = var.web_domain_name
  delegation_set_id = var.delegation_set_id
}

resource "aws_route53_record" "cloudfront" {
  count   = length(var.distribution_aliases)
  name    = var.distribution_aliases[count.index]
  zone_id = aws_route53_zone.linhhn508.zone_id
  type    = "A"

  alias {
    name                   = var.distribution_name
    zone_id                = var.distribution_zone_id
    evaluate_target_health = false
  }
}