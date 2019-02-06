# Description
On the process of executing a request, the Visualizer component leverages existing tools to provide rich visualizations of the applications being run by Asperathos.

# Architecture
The visualizer is implemented following a plugin architecture, providing flexibility to add or remove plugins when necessary. All the integrations with different infrastructures and components are made by specific plugins, so the different technologies in the context of EUBra-BIGSEA framework can be easily integrated by the visualizer service.
