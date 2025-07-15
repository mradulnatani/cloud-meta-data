# cloud-meta-data (for ssh-authority)

A lightweight Python utility to fetch and inspect metadata from AWS EC2 virtual machines.  
This is designed to work with the [ssh-authority](https://github.com/mradulnatani/ssh-authority) project for automated SSH certificate issuance.

## Overview

`cloud-meta-data` collects identity-related information (e.g., instance ID, region, hostname) from the EC2 instance metadata service and forwards it to the `ssh-authority` server.
This helps automate SSH certificate-based access control in cloud environments, improving security and simplifying key management.

## Installation

### 1. Clone the repository
````bash
git clone https://github.com/mradulnatani/cloud-meta-data.git
````
### 2. Set executable permission and install dependencies

```bash
cd cloud-meta-data
chmod +x ./initial.sh
./initial.sh
```

This script installs required Python packages and prepares the environment.

### 3. Run the metadata agent

```bash
python3 server-data.py
```

This will collect instance metadata and send it to the configured `ssh-authority` server.

---

## Supported Cloud Providers

*  Amazon Web Services (EC2)

---

## Use Case with ssh-authority

This project integrates with [`ssh-authority`](https://github.com/mradulnatani/ssh-authority) to:

* Register cloud VMs automatically for SSH access
* Issue short-lived SSH certificates tied to machine identity
* Eliminate the need for static public key trust setup

---

## Directory Structure

```
cloud-meta-data/
├── initial.sh           # Environment setup script
├── server-data.py       # Main metadata collection + sender
├── README.md            # This documentation
```

This project is licensed under the [MIT License](LICENSE). <br/>
Made by [@mradulnatani](https://github.com/mradulnatani)

