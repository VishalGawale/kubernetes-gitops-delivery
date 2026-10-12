resource "kubernetes_namespace_v1" "env" {
  for_each = toset(["dev", "prod", "monitoring"])

  metadata {
    name = each.key
  }
}