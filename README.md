# 🔐 Secure Document Manager

A cloud-based document management web application deployed on **Amazon EC2** and integrated with **Amazon S3** for secure document storage.

The application allows users to upload, view, download, and delete documents stored in a **private S3 bucket**. Access to AWS resources is managed using **IAM-based permissions**.

---

## 📌 Project Overview

The **Secure Document Manager** is a web application designed to provide a simple and secure way to manage documents using AWS cloud services.

The application is hosted on an **Amazon EC2 instance** and uses a **private Amazon S3 bucket** as the document storage layer.

The project demonstrates practical implementation of:

- Cloud deployment
- Amazon EC2
- Amazon S3
- AWS IAM
- Linux server management
- Python web development
- Git and GitHub
- Basic cloud security

---

## 🚀 Features

- 📤 Upload documents to Amazon S3
- 📂 View uploaded documents
- ⬇️ Download documents
- 🗑️ Delete documents
- 📏 Maximum file size of 10 MB
- 📊 Display file size
- 🕒 Display document modified date/time
- 🔒 Private S3 storage
- 🔐 IAM-based AWS access
- ☁️ Application deployed on Amazon EC2

---

## 🛠️ Technologies Used

### Application

- Python
- Flask
- HTML
- CSS

### AWS Services

- **Amazon EC2** – Application hosting
- **Amazon S3** – Document storage
- **AWS IAM** – Access control and permissions

### Development & Deployment

- Linux
- Git
- GitHub
- Gunicorn
- Nginx

---

## ☁️ AWS Architecture

```text
                 👤 User
                    |
                    v
          ┌──────────────────┐
          │ Secure Document  │
          │     Manager      │
          │   Web Interface  │
          └────────┬─────────┘
                   |
                   v
            ┌─────────────┐
            │ Amazon EC2  │
            │   Server    │
            └──────┬──────┘
                   |
              IAM Access
                   |
                   v
          ┌─────────────────┐
          │  Private S3     │
          │     Bucket      │
          └────────┬────────┘
                   |
                   v
              📄 Documents
