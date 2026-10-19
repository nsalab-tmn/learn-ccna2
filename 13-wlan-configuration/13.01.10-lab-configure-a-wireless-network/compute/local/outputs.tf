# These outputs become tf-dynamic-params.json (raw `terraform output` envelope),
# read by learn-assessment. The address is the container's learn-labs IP / DNS name
# — an assessment-reachable address on the shared network, NEVER localhost (the
# grader runs in a sibling container on learn-labs).

output "lab_host" {
  description = "Docker DNS name (= container name) on learn-labs."
  value       = docker_container.lab.name
}

output "lab_ip" {
  description = "Container IP on the learn-labs network (never localhost)."
  value = one([
    for n in docker_container.lab.network_data : n.ip_address
    if n.network_name == "learn-labs"
  ])
}

output "ssh_port" {
  description = "Legacy alias: SSH port of the first simulated device (ISP)."
  value       = 22
}

# One SSH port per simulated device: the base port + its topology id (read from
# topology.yaml, so reordering the devices can't silently break grading). Output
# names are static in Terraform: add one block per simulated device.
output "ssh_port_ISP" {
  description = "SSH port of ISP (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["ISP"]
}

output "ssh_port_WebServer" {
  description = "SSH port of WebServer (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["WebServer"]
}

output "ssh_port_WR" {
  description = "SSH port of WR (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["WR"]
}

output "ssh_port_Admin" {
  description = "SSH port of Admin (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["Admin"]
}

output "ssh_port_Laptop1" {
  description = "SSH port of Laptop1 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["Laptop1"]
}

output "ssh_port_Laptop2" {
  description = "SSH port of Laptop2 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["Laptop2"]
}

output "ssh_port_AP" {
  description = "SSH port of AP (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["AP"]
}

output "ssh_port_Laptop3" {
  description = "SSH port of Laptop3 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["Laptop3"]
}

output "URL" {
  description = "Student web canvas (topology + in-page device console) — the platform edge proxies this to the learner."
  value       = "http://${docker_container.lab.name}:7681/"
}

output "ssh_user" {
  description = "SSH username."
  value       = "admin"
}

output "ssh_password" {
  description = "Per-lab SSH password."
  value       = random_password.ssh.result
  sensitive   = true
}
