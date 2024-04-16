
# Modularity

Depictio is designed with a modular architecture, allowing for easy integration of new features and functionalities. The frontend and backend components are decoupled, enabling independent development and deployment of each module. The platform is built to be scalable and adaptable to various needs, with a focus on user-friendly interfaces and interactive data visualization tools. 

The code organisation clearly separates each of the frontend components and the API endpoints, making it easy to understand and extend the platform.

## Dashboard components

Each of the components is designed to be modular and can be easily integrated into the dashboard. To add a new component to the dashboard, you simply need to click on the "Add new component" button of your dashboard. This will open a 3-levels modal where you will be able to select:

1. The data source: it corresponds to the bioinformatics workflow and the data collection you want to be based on to build your new component.
  
2. The component type: it corresponds to the type of component (listed below) you want to add to your dashboard.

3. The component configuration: it corresponds to the configuration of the component you want to add to your dashboard.

### Generic components (Data collection Table)
There are currently 4 main components supported to build your dashboard:

* Figures: Bar, Line, Scatter, Box and Histogram plots.
* Metrics cards: Cards displaying metrics values.
* Interactive components: (slider, dropdown, input text, etc.)
* Tables: Interactive tables with sorting, filtering and searching functionalities.

### Specific components
* JBrowse: Genome browser to visualize genomic data.
* Graphs: Network graphs to visualize interactions between entities.
* Geomap: Geographical map.