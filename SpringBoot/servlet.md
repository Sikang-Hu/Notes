# Embeded Tomcat
## Configuration
1. just configure our server
   ```properties
   server.port=8081
   server.context-path=/crud

   // configuration for Servlet
   server.xxx

   // configuration for Tomcat
   server.tomcat.xxx
   ```
   There is a class called **ServerProperties** which defines all available configuration.

2. Write a **EmbeddedServletContainerCustomizer**:
   ```java
   @Bean
   public EmbeddedServletContainerCustomizer embeddedServletContainerCustomizer() {
       return new EmbeddedServletContainerCustomizer() {
           @Override
           public void customize(ConfigurableEmbeddedServletContainer container) {
               container.setPort(8083);
           }
       }
   }
   ```

   