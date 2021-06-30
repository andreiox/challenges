const memoize = require("memoizee");
const sleep = require("async-sleep");
const hash = require("object-hash");

const fn = async function (data, hello) {
  console.log("function performed");
  await sleep(500);
  return `${data.one}${data.two}${hello}`;
};

const normalizer = (args) => hash(args[0]);

memoized = memoize(fn, { promise: true, maxAge: 2000, normalizer });

const hello = memoized({ one: "foo", two: 3 }, "bar");
const hi = memoized({ one: "foo", two: 3 }, "bar");

hello.then(console.log).catch(console.log); // resolved at the same time
hi.then(console.log).catch(console.log); // resolved at the same time

sleep(2000).then((res) => {
  const hello2 = memoized({ one: "foo", two: 3 }, "bar");
  hello2.then(console.log).catch(console.log); // cache hit
});

sleep(3000).then((res) => {
  const hello2 = memoized({ one: "foo", two: 3 }, "bar");
  hello2.then(console.log).catch(console.log); // no cache hit
});
