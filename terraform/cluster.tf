resource "kind_cluster" "this" {
  name           = "ai-platform"
  node_image     = "kindest/node:v1.34.3"
  wait_for_ready = true

  kind_config {
    kind        = "Cluster"
    api_version = "kind.x-k8s.io/v1alpha4"

    node {
      role = "control-plane"
    }
  }
}