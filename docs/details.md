# Description
On the process of executing a request, the visualizer is responsible for launch a visualizer application and set up this application for the application that is running.

# Architecture
The visualizer is implemented following a plugin architecture, providing flexibility to add or remove plugins when necessary. All the integrations with different infrastructures and components are made by specific plugins, so the different technologies in the context of EUBra-BIGSEA framework can be easily integrated by the visualizer service.
