# Define Index Name through Environment Variables

You may need to define the elasticsearch search according to the running cases, say for different client. Hence you want to set the index name dynamically here are two solution.

## 1

1. Create a Bean returning a value for some property.

    ```java
    @Bean
    public String somePropertyValue() {
        return System.getenv("some-property");
    }
    ```

2. Then, you can retrieve it at `@Document`:

```java
@Document(indexName="#{@somePropertyValue}")
public class Book {
    // Your object relational mapping
}
```

## 2

1. Create a pair of setter and getter in bean:

    ```java
    @Component
    public class Config() {

        @Value("${env.somePropertyValue}")
        private String somePropertyValue;

        public String getSomePropertyValue() {
            return somePropertyValue;
        }

        public void setSomePropertValue() {
            this.somePropertyValue = somePropertyValue;
        }
    }
    ```

2. Then, access it in `@Document`:

    ```java
    @Document(indexName="#{config.somePropertyValue}")
    public class Book {
        // Your object relational mapping
    }
    ```
