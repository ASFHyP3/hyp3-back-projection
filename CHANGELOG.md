# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [PEP 440](https://www.python.org/dev/peps/pep-0440/)
and uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.2]

### Fixed
* `back_project` granules parameter so that it can accept a string of space-delimited granule names.

## [0.5.1]

### Fixed
* Main Dockerfile so that workflow matches changes introduced by fixing GPU workflow.

### Changed
* Main Dockerfile to use a multi-stage build, mirroring Dockerfile.gpu.

## [0.5.0]

### Added
* `scripts/ubuntu_setup.sh` for setting up a GPU-based Ubuntu EC2 AMI.
* `scripts/amazon_linux_setup.sh` for setting up a GPU-based Amazon Linux 2023 EC2 AMI.

### Changed
* Refactored `scripts/build_proc.sh` to combine GPU compilation steps.
* Final product zip archive is now always created.

### Fixed
* `Dockerfile.gpu` so that outputs will contain actual data.

## [0.4.0]

### Added
* Support for GPU accelerated processing using CUDA.

## [0.3.0]

### Added
* Compilation of the `back-processing` code to the Dockerfile.
* CPU-based workflow for back-projecting level-0 Sentinel-1 data

### Changed
* Compilation script now uses libfftw3f library installed using `apt` instead of locally compiled version.

## [0.2.0]

### Added
* Created a fresh version of the repository using hyp3-cookiecutter.

### Removed
* All the files associated with the pre-2021 work, except the .git folder.

## [0.1.0]

### Added
* All pre-2021 work on the repository.

## [0.0.0]

### Added
* Initial version of repository.

