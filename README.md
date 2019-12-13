<!-- PROJECT LOGO -->
<br />
<p align="center">

  <h1 align="center">ECC based Authentication</h1>

  <p align="center">
    A secure elliptic curve cryptography based mutual authentication
protocol for cloud-assisted TMIS
    <br />
    <br />
    <a href="https://github.com/RikilG/ECC-Based-Authentication/issues">Report Bug</a>
    ·
    <a href="https://github.com/RikilG/ECC-Based-Authentication/issues">Request Feature</a>
  </p>
</p>


## Table of Contents

- [Table of Contents](#table-of-contents)
- [About The Project](#about-the-project)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Dependencies](#dependencies)
- [License](#license)
- [Team Members](#team-members)
- [Acknowledgements](#acknowledgements)


## About The Project

This repository implements the steps given by the ECC model proposed by Kumar, V., Ahmad, M., Kumari, A., [A Secure Elliptic Curve Cryptography Based Mutual Authentication Protocol for Cloud-assisted TMIS, Telematics and Informatics (2018)](https://doi.org/10.1016/j.tele.2018.09.001),
and provides analysis w.r.t previous crypto system proposed by [Li et al](https://doi.org/10.1016/j.cmpb.2018.02.002).

The main aim of this project is to simulate a system similar to the proposed protocol. Therefore, the model implements all the required steps given in the protocol and shows its working without relying on a network based model.

Built With [Python](https://www.python.org)


## Getting Started

To get a local copy up and running follow these steps:

### Prerequisites

```sh
sudo apt install python3 # if python is not installed
pip install pycryptodome # make sure pip supports python 3 and not python 2
```

### Installation
 
1. Clone this repo
```sh
git clone https://github.com/RikilG/ECC-Based-Authentication.git
cd ECC-Based-Authentication
```
2. Run program
```sh
cd src/proposed #for running proposed protocol
python main.py
```

### Dependencies

List of dependencies present/used in the project
 - [pycryptodome](https://pycryptodome.readthedocs.io)
 - [hashlib](https://docs.python.org/3/library/hashlib.html)
 - [random](https://docs.python.org/3/library/random.html)

## License

Code distributed under the MIT License. See `LICENSE` for more information.

## Team Members

Project implemented by:
* [Rikil Gajarla](https://github.com/RikilG) - 2017A7PS0202H
* [Badri Vishal Kasuba](https://github.com/kasuba-badri-vishal) - 2017A7PS0270H
* [Raj Kashyap Mallela](https://github.com/https://github.com/Rajkashyapmallala) - 2017A7PS0025H

Project Link: [https://github.com/RikilG/ECC-Based-Authentication](https://github.com/RikilG/ECC-Based-Authentication)


## Acknowledgements

* [Bits Pilani Hyderabad Campus](https://www.bits-pilani.ac.in/Hyderabad/) for providing us with access to journals and research papers.
* [f47h3r/CryptoWrapper](https://github.com/f47h3r/CryptoWrapper) for providing a all-in-one crypto wrapper.