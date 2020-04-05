# SpringBoot Note-Error Handle
## Auto Configuration: **ErrorMvcAutoConfiguration**
1.  DefaultErrorAttributes: Help to store attributes
   - timestamp
   - status
   - error
   - exception
   - message
   - error
2.  BasicErrorController: handle the "/error" request
    ```java
    @RequestMapping(produces = "text/html")
    public ModelAndView errorHtml(HttpServletRequest request, HttpServletResponse response) {
        //Generate the response in HTML
    }

    @RequestMapping
    @ResponseBody
    public ReponseEntity<Map<String, Object>> error(HttpServletRequest request) {
        //Generate the response in JSON
    }
    ```
3.  ErrorPageCustomizer:  
    ```java
    @Value("${error.path:/error}")
    private String path = "/error";
    ```
   If there is error, it will redirect to **/error** for handling
   
4.  DefaultErrorViewResolver: Find the viewName under error/, use the Template to resolve it  
    ```java
    TemplateAvailabilityProvider provider = this.templateAvailabilityProviders.getProvider(errorViewName, this.applicationContext);
    ```

   If Template is unavailable, it will find corresponding page under static resource folder.

```
Process: 

If there is 4xx or 5xx error, ErrorPageCustomizer will be in effect. Then BasicErrorController will handle the "/error" request. Then, the DefaultErrorViewResolver will try to find corresponding resouce under error/ or in the static resource folder.
```

## How to customize error data
1. Rewrite customized Exception and Exception Handler, use the **@Exceptionhandler**
   ```java
   @ResponseBody
   @ExceptionHandler(UserNotExistException.class)
   public Map<String, Object> handleException(Exception e) {
       //...
   }
   // However, in this case, it will always return in the format of JSON
   ```
2. Set the fields in the HttpServletRequest object and then forwards the request to **/error**.
   ```java
   @ResponseBody
   @ExceptionHandler(UserNotExistException.class)
   public Map<String, Object> handleException(Exception e, HttpSevletRequest request) {
       //...
       request.setAttribute("javax.servlet.error.status_code", 400);
       //...
       return "forward:/error";
   }
   ```
3. Pass the customized data: when the request is forwarded to **/error** it will be handled by **BasicErrorController**, which accesses data through *getErrorAttributes()* which is a method defined in **AbstractBasicController**. So, we can write our own class to extend it and override the *getErrorAttributes()*.<br/><br/>
However, we also have another easier method. Since the *getErrorAttributes()* acquire the attributes from *errorAttributes*, a **ErrorAttributes** object, we can define our own **ErrorAttributes**:
    ```java
    @Component
    public class MyErrorAttributes extends DefaultErrorAttributes {
        @Overide
        public Map<String, Object> getErrorAttributes(RequestAttributes requestAttributes, boolean includeStackTrace) {
            Map<String, Object> map = super.getErrorAttributes(requestAttributes, includeStackTrace);
            map.put("company", "philips");

            Map<String, Object> ext = (Map<String, Object>) requestAttributes.getAttribute("ext", 0);

            map.put("ext", ext);

            return map;
        }
    }
    ```
 