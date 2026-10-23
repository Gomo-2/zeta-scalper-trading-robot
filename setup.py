from setuptools import setup, find_packages

setup(
    name="zeta-scalper",
    version="0.1.0",
    description="Educational zeta scalper trading robot for backtesting and paper trading.",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pandas>=2.0.0",
        "numpy>=1.26.0",
        "requests>=2.31.0",
    ],
)
