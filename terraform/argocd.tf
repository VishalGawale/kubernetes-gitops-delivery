resource "helm_release" "argocd" {
  name             = "argocd"
  repository       = "https://argoproj.github.io/argo-helm"
  chart            = "argo-cd"
  version          = "10.10.3"
  namespace        = "argocd"
  create_namespace = true
  timeout          = 600

  values = [yamlencode({
    dex           = { enabled = false }
    notifications = { enabled = false }
    server = {
      livenessProbe  = { timeoutSeconds = 5 }
      readinessProbe = { timeoutSeconds = 5 }
    }
    repoServer = {
      livenessProbe  = { timeoutSeconds = 5 }
      readinessProbe = { timeoutSeconds = 5 }
    }
  })]
}
