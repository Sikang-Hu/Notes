# Learning Note

A note recording miscellaneous tips for Angular

## Using index in iteration in HTML

```html
<ul>
    <li *ngFor="let item of list;let key = index;">
        {{key}} -- {{item.name}}
    </li>
</ul>
```

## Modified CSS dynamically

Use `[ngClass]` or `[ngStyle]`

```html
<div [ngClass]="{'red':flag, 'red':!flag}">
    <!-- your content -->
    <!-- flag is a variable that can be changed dynamically -->
</div>
```

## Pipeline

```html
<h1>Pipeline</h1>
{{today | data:'yyyy-MM-dd HH:mm:ss'}}
```

## Event

```html
<button (click)="run()"></button>
```

```html
<input type="text" (keydown)="keyDown($event)" />

<input type="text" (keyup)="keyDown($event)" />
```

If using keydown, event.target.value will not contains the last typed character, if you want to include the latest input, use keyup instead.

## forEach is async, may leads to 