# JavaScript async/fetch Reference (from javascript.info)

Excerpted from the Modern JavaScript Tutorial (javascript.info) https://javascript-tutorial/en.javascript.info.

## Fetch error handling with async/await

```javascript
async function loadJson(url) {
  let response = await fetch(url);

  if (response.status == 200) {
    let json = await response.json();
    return json;
  }

  throw new Error(response.status);
}
```

## Fetch error handling with try/catch

```javascript
async function f() {
  try {
    let response = await fetch('http://no-such-url');
  } catch(err) {
    alert(err); // TypeError: failed to fetch
  }
}
```

## Promise chain error handling

```javascript
fetch('https://no-such-server.blabla') // rejects
  .then(response => response.json())
  .catch(err => alert(err)) // TypeError: failed to fetch (the text may vary)
```

## Multiple async operations in one try/catch

```javascript
async function f() {
  try {
    let response = await fetch('/no-user-here');
    let user = await response.json();
  } catch(err) {
    // catches errors both in fetch and response.json
    alert(err);
  }
}
```

## Top-level async error with .catch()

```javascript
async function f() {
  let response = await fetch('http://no-such-url');
}
f().catch(alert);
```

## Sending data with fetch (POST)

```javascript
fetch('https://api.github.com/repos/javascript-tutorial/en.javascript.info/commits', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ data }),
})
  .then(response => response.json())
  .then(result => console.log(result));
```

## Fetch options and GET request

```javascript
let url = 'https://api.github.com/repos/javascript-tutorial/en.javascript.info/commits';
let response = await fetch(url);

if (response.ok) {
  let json = await response.json();
} else {
  alert("HTTP-Error: " + response.status);
}
```

## Loading JSON with async/await

```javascript
let url = 'https://api.github.com/repos/javascript-tutorial/en.javascript.info/commits';
let response = await fetch(url);
let commits = await response.json();

alert(commits[0].author.login);
```

## Source

- The Modern JavaScript Tutorial: https://javascript-tutorial/en.javascript.info
- Async/Await reference: https://javascript.info/async-await
- Fetch API reference: https://javascript.info/fetch
