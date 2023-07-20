<div align="center">

# [mndotbidprices.com](https://mndotbidprices.com)

*An analytics dashboard for exploring construction bids on Minnesota Department of Transportation (MnDOT) projects.*

[![item search preview](static/item-search-preview.png)](https://mndotbidprices.com)
</div>

## Introduction

Estimating the cost of a proposed construction project is often a difficult task for engineers. The factors impacting the cost of each unit of work are many and difficult to fully account for. Engineers often rely on cost data from past projects to inform their estimates. Sources such as MnDOT's own [Average Bid Price](https://edocs-public.dot.state.mn.us/edocs_public/DMResultSet/Urlsearch?columns=docnumber,docname,app_id&folderid=28521650) documents help with this, but often leave the user wanting for more recent and detailed information.

This dashboard provides those recent and detailed insights by scraping data from individual [contract award abstracts](https://www.dot.state.mn.us/bidlet/abstract.html) and providing summary statistics computed from that data.

## Usage

A hosted version of the dashboard is available at [mndotbidprices.com](https://mndotbidprices.com). See the dashboard's *Usage* section for detailed instructions for operating the application.

## Installation

The dashboard (frontend) and data pipeline (backend) can be installed and hosted locally. There is no direct communication between the frontend and backend, so they do not need to be installed or ran concurrently. See the READMEs in the respective directories for installation instructions

[Frontend README](https://github.com/depowered/mndot-bid-v2/frontend/)

[Backend README](https://github.com/depowered/mndot-bid-v2/backend/)

## [License](LICENSE)

MIT &copy; 2023 [Devin Power](https://github.com/depowered)