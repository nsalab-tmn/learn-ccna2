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
  description = "Legacy alias: SSH port of the first simulated device (Home-Wireless-Router)."
  value       = 22
}

# One SSH port per simulated device: the base port + its topology id (read from
# topology.yaml, so reordering the devices can't silently break grading). Output
# names are static in Terraform: add one block per simulated device.
output "ssh_port_Home-Wireless-Router" {
  description = "SSH port of Home-Wireless-Router (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["Home-Wireless-Router"]
}

output "ssh_port_Tablet-PC" {
  description = "SSH port of Tablet-PC (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["Tablet-PC"]
}

output "ssh_port_Smartphone" {
  description = "SSH port of Smartphone (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["Smartphone"]
}

output "ssh_port_Laptop" {
  description = "SSH port of Laptop (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["Laptop"]
}

output "ssh_port_Home-Admin" {
  description = "SSH port of Home-Admin (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["Home-Admin"]
}

output "ssh_port_Router0" {
  description = "SSH port of Router0 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["Router0"]
}

output "ssh_port_DNS-Server" {
  description = "SSH port of DNS-Server (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["DNS-Server"]
}

output "ssh_port_Web-Server" {
  description = "SSH port of Web-Server (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["Web-Server"]
}

output "ssh_port_R1" {
  description = "SSH port of R1 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["R1"]
}

output "ssh_port_RADIUS-Server" {
  description = "SSH port of RADIUS-Server (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["RADIUS-Server"]
}

output "ssh_port_SW1" {
  description = "SSH port of SW1 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["SW1"]
}

output "ssh_port_Admin-PC" {
  description = "SSH port of Admin-PC (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["Admin-PC"]
}

output "ssh_port_WLC-1" {
  description = "SSH port of WLC-1 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["WLC-1"]
}

output "ssh_port_LAP-1" {
  description = "SSH port of LAP-1 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["LAP-1"]
}

output "ssh_port_Laptop1" {
  description = "SSH port of Laptop1 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["Laptop1"]
}

output "ssh_port_Laptop-2" {
  description = "SSH port of Laptop-2 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["Laptop-2"]
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
