# Valorant Customs Stats
Dashboard statistics tracking of DARWIN discord custom games. Using Power BI and VBA to automate data cleaning and visualization. 

![Dashboard](https://github.com/candysan7/valorant-customs-stats/blob/main/images/version1.1.png)

## Power BI Dashboard Report 

[Click To See Dashboard](https://app.powerbi.com/view?r=eyJrIjoiNGUzNzMyOTctNTg2OC00YTEyLThmNjktOTJiOTE3ZGM0NjI3IiwidCI6IjlkZGFhY2ExLTM4OWYtNGNiMS1hMTEzLTA4MWJlNmNjMjVmYyIsImMiOjZ9)

## Data 
| Dataset                            | Description                                                                    |
| :--------------------------------- | :----------------------------------------------------------------------------- |
| `data.csv`                         | Raw data                                                                       |
| `individual.csv`                   | Individual win-rate and fraction of games won                                  |
| `teammate-synergy.csv`             | Win-rate when with a specific player on your team                              |
| `easiest-matchups.csv`             | Win-rate when a specific player is on the opposite team                        |
| `maps.csv`                         | Map playtime                                                                   |
| `winrate-over-time.csv`            | Individual win-rate in two-week blocks, starting on October 3rd, 2022          |
| `cumulative-winrate-over-time.csv` | Cumuluative individual win-rate every two weeks, starting on October 3rd, 2022 |

## Documentation

### Architecture & Design 

![Architecture](https://github.com/candysan7/valorant-customs-stats/blob/main/images/architecture4.png)

### Future improvements
- Automate "Last Updated" text
- Build discord bot or command to return dashboard link
- Convert cumulative average to 60-day moving average

### Why Power BI over Tableau? 
- Tableau was not able to display string and integer values on the same table 
- Power BI also allows for **free** desktop version 

### Credits

| Contributor              | Role                    |
| :------------------------| :-----------------------|
| **Lindsey Wong**         | Back-end Developer      |
| **Andy Xiang**           | Front-end Developer     |
| **Steven Truong**        | Product Manager         |
