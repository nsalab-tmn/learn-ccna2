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
  description = "Legacy alias: SSH port of the first simulated device (Edge-Router)."
  value       = 22
}

# One SSH port per simulated device: the base port + its topology id (read from
# topology.yaml, so reordering the devices can't silently break grading). Output
# names are static in Terraform: add one block per simulated device.
output "ssh_port_Edge-Router" {
  description = "SSH port of Edge-Router (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["Edge-Router"]
}

output "ssh_port_ISP" {
  description = "SSH port of ISP (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["ISP"]
}

output "ssh_port_Server" {
  description = "SSH port of Server (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["Server"]
}

output "ssh_port_L3-SW1" {
  description = "SSH port of L3-SW1 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["L3-SW1"]
}

output "ssh_port_Sw-A" {
  description = "SSH port of Sw-A (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["Sw-A"]
}

output "ssh_port_Sw-B" {
  description = "SSH port of Sw-B (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["Sw-B"]
}

output "ssh_port_Sw-C" {
  description = "SSH port of Sw-C (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["Sw-C"]
}

output "ssh_port_WS-1-1" {
  description = "SSH port of WS-1-1 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["WS-1-1"]
}

output "ssh_port_WS-1-2" {
  description = "SSH port of WS-1-2 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["WS-1-2"]
}

output "ssh_port_WS-1-3" {
  description = "SSH port of WS-1-3 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["WS-1-3"]
}

output "ssh_port_WS-1-4" {
  description = "SSH port of WS-1-4 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["WS-1-4"]
}

output "ssh_port_WS-1-5" {
  description = "SSH port of WS-1-5 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["WS-1-5"]
}

output "ssh_port_WS-1-6" {
  description = "SSH port of WS-1-6 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["WS-1-6"]
}

output "ssh_port_WS-2-1" {
  description = "SSH port of WS-2-1 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["WS-2-1"]
}

output "ssh_port_WS-2-2" {
  description = "SSH port of WS-2-2 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["WS-2-2"]
}

output "ssh_port_WS-2-3" {
  description = "SSH port of WS-2-3 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["WS-2-3"]
}

output "ssh_port_Management-PC" {
  description = "SSH port of Management-PC (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["Management-PC"]
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
