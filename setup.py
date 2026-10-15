from setuptools import setup, find_packages

setup(
    name="magic-hat",
    version="1.0.0",
    description="Mobile offensive security and reconnaissance framework for Termux/NetHunter",
    author="Magician",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    install_requires=[
        "flask>=2.0.0",
    ],
    entry_points={
        "console_scripts": [
            "magic-hat=magic_hat.main:main",
        ],
    },
    python_requires=">=3.6",
)
