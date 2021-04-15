# SpringBoot Note

## 1 @SpringBootTest annotation prevent the RestTemplate to be injected

## Spring Beans and Dependency Injection

@ComponentScan will register all the components(@Component, @Service, @Repository, @Controller etc.) automatically.

When bean has one constuctor, the @Autowired can be omitted.

```java
@Service
public class DatabaseAccountService implements AccountService {
    private final RiskAssessor riskAssessor;

    public DatabaseAccountService(RiskAssessor riskAssesor) {
        this.riskAssessor = riskAssessor;
    }
}
```

In this senario, you can stablish final field.

## @SpringBootApplication

Enable three features:

* @EnableAutoConfiguration
  
* @ComponentScand: @ComponentScan on package where the application is located
  
* @Configuration: allow to register extra beans in the context or import additonal configuration classes

