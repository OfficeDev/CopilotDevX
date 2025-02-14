This repository contains sample agentic applications in python that can talk to Azure AI and OpenAI models and perform complex tasks based on user queries.

## Prerequisites

1. You need an OpenAI API Key, Tavily Search API Key, Open Weather Map API Key and M365 Developer Tenant
2. You will need to buy a license to use the OpenAI GPT models
3. Alternatively, you can use AzureAI models by deploying your models using your Azure subscription. Steps are here --> https://learn.microsoft.com/en-us/azure/ai-foundry/model-inference/concepts/endpoints?tabs=python
4. You will need to create an app registration in Azure portal. Use the following steps - https://learn.microsoft.com/en-us/graph/tutorials/python?tabs=aad&tutorial-step=1
5. Save the ClientID and the TenantID from this app you created.
6. You need to install Python, Jupyter notebook, PIP on your system. I am using Windows 11.
7. You need to install the following Python Packages - Jupyter, Python, LangChain, MSGraph, AzureIdentity

## Steps to get your first Agent running

1. Clone this repository
2. Go to the folder where you downloaded the repository.
3. Open the .env file and add your keys that you obtained from OpenAI, Tavily, Open Weather Map, etc.
4. Add ClientID and the TenantID
5. Save and Close the file.
6. Run the following command to ensure all the right libraries are installed --> pip install --requirement=.\requirements.txt
7. Open Command Prompt and go to the folder where the repository is.
8. Type the following command - jupyter notebook
9. This will open a web page that contains all your scripts.
10. Click on first Agent script and it will open in a separate page.
11. Click on the run icon.
12. You should see the output on the line below.
13. Getting the Clippy2 Agent running This is a more advanced Agent and to run it, you will need to access Microsoft Graph SDKs.

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
