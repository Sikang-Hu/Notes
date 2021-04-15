# Angular Concept

Angular is a platform for building SPA using HTML and TypeScript

## Modules

`@NgModule()`

Angular NgModules declares a compliation context for a set of components. It can associate its components with related code, such as service, to form functional units.

Every Angular app has a root module, named AppModule by default, which provides bootstrap mechanism that launch the app. Besides, an app also contains many funcitonal module.

You can import other NgModules to use their functionality.

## Component

`@Component()`

Every Angular app has at least one component, the root component that connects a component hierachy with the DOM. Each component defines a class that contains app's data and logic and is associated with an HTML template that defines a view to be displayed in a target environment.

## Template

Template combines HTML with Angular markup. Template directive provide program logic, and binding markup connects your application data and the DOM.

## Route