This repository contains sample agentic applications in python that can talk to OpenAI models and perform complex tasks based on user queries.

##Prerequisites

You need an OpenAI API Key, Tavily Search API Key, Open Weather Map API Key and M365 Developer Tenant
You will need to buy a license to use the OpenAI GPT models
Alternatively, you can use AzureAI models by deploying your models using your Azure subscription. Steps are here --> https://learn.microsoft.com/en-us/azure/ai-foundry/model-inference/concepts/endpoints?tabs=python
You will need to create an app registration in Azure portal. Use the following steps - https://learn.microsoft.com/en-us/graph/tutorials/python?tabs=aad&tutorial-step=1
Save the ClientID and the TenantID from this app you created.
You need to install Python, Jupyter notebook, PIP on your system. I am using Windows 11.
You need to install the following Python Packages - Jupyter, Python, LangChain, MSGraph, AzureIdentity

##Steps to get your first Agent running

Clone this repository
Go to the folder where you downloaded the repository.
Open the .env file and add your keys that you obtained from OpenAI, Tavily, Open Weather Map, etc.
Add ClientID and the TenantID
Save and Close the file.
Run the following command to ensure all the right libraries are installed --> pip install --requirement=.\requirements.txt
Open Command Prompt and go to the folder where the repository is.
Type the following command - jupyter notebook
This will open a web page that contains all your scripts.
Click on first Agent script and it will open in a separate page.
Click on the run icon.
You should see the output on the line below.
Getting the Clippy2 Agent running This is a more advanced Agent and to run it, you will need to access Microsoft Graph SDKs.

## Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft 
trademarks or logos is subject to and must follow 
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.
