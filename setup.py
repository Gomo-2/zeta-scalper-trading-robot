from setuptools import setup, find_packages

setup(
    name="zeta-scalper",
    version="0.1.1",
    description="Educational zeta scalper trading robot with broker/exchange adapter support.",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pandas>=2.0.0",
        "numpy>=1.26.0",
        "requests>=2.31.0",
    ],
    entry_points={
        "console_scripts": [
            "zeta-scalper=zeta_scalper.cli:main",
        ]
    },
)
