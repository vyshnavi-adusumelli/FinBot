from setuptools import setup, find_packages

setup(
    name='MyDollarBot',
    version='1.0.0',
    packages=find_packages(),
    description='Telegram bot to manage expenses',
    tests_require=['pytest'],
    author='CSC510 - Group 21',
    author_email='mydollarbot@gmail.com',
    url='https://github.com/mtkumar123/MyDollarBot',
    python_requires='>=3.7',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Intended Audience :: Developers",
        "Topic :: MyDollarBot",
    ],
    license='MIT',
    install_requires=[
        'pyTelegramBotAPI==4.1.0',
        'pandas==1.3.4'
    ]
)
