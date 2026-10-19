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
  description = "Legacy alias: SSH port of the first simulated device (MLS)."
  value       = 22
}

# One SSH port per simulated device: the base port + its topology id (read from
# topology.yaml, so reordering the devices can't silently break grading). Output
# names are static in Terraform: add one block per simulated device.
output "ssh_port_MLS" {
  description = "SSH port of MLS (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["MLS"]
}

output "ssh_port_SW-1" {
  description = "SSH port of SW-1 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["SW-1"]
}

output "ssh_port_SW-2" {
  description = "SSH port of SW-2 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["SW-2"]
}

output "ssh_port_PC-101" {
  description = "SSH port of PC-101 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["PC-101"]
}

output "ssh_port_PC-102" {
  description = "SSH port of PC-102 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["PC-102"]
}

output "ssh_port_PC-110" {
  description = "SSH port of PC-110 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["PC-110"]
}

output "ssh_port_PC-124" {
  description = "SSH port of PC-124 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["PC-124"]
}

output "ssh_port_PC-201" {
  description = "SSH port of PC-201 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["PC-201"]
}

output "ssh_port_PC-202" {
  description = "SSH port of PC-202 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["PC-202"]
}

output "ssh_port_PC-210" {
  description = "SSH port of PC-210 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["PC-210"]
}

output "ssh_port_PC-224" {
  description = "SSH port of PC-224 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["PC-224"]
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

output "URL" {
  description = "Student web canvas (topology + in-page device console) — the platform edge proxies this to the learner."
  value       = "http://${docker_container.lab.name}:7681/"
}
