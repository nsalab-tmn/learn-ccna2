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
  description = "Legacy alias: SSH port of the first simulated device (Edge_Router)."
  value       = 22
}

# One SSH port per simulated device: the base port + its topology id (read from
# topology.yaml, so reordering the devices can't silently break grading). Output
# names are static in Terraform: add one block per simulated device.
output "ssh_port_Edge_Router" {
  description = "SSH port of Edge_Router (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["Edge_Router"]
}

output "ssh_port_ISP1" {
  description = "SSH port of ISP1 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["ISP1"]
}

output "ssh_port_ISP2" {
  description = "SSH port of ISP2 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["ISP2"]
}

output "ssh_port_ISP_LAN" {
  description = "SSH port of ISP_LAN (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["ISP_LAN"]
}

output "ssh_port_Customer-Server" {
  description = "SSH port of Customer-Server (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["Customer-Server"]
}

output "ssh_port_LAN_1" {
  description = "SSH port of LAN_1 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["LAN_1"]
}

output "ssh_port_LAN_2" {
  description = "SSH port of LAN_2 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["LAN_2"]
}

output "ssh_port_PC-A" {
  description = "SSH port of PC-A (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["PC-A"]
}

output "ssh_port_PC-B" {
  description = "SSH port of PC-B (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["PC-B"]
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
