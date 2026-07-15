---
title: "HoWA"
up: "[[Entities/Projects/HoWA]]"
date: "2026-07-15"
updated: "2026-07-15"
tags: ["projects"]
category: "projects"
---

↑ [[Entities/Projects/HoWA|HoWA]]


## Links

- [[Projects/HoWA]]
- [[Entities/Projects/HoWA]]

Let's create a ETF System management - done

I want to intreduce lazy-loading system to most of the queried data, as currently I'm loading all data at once which causes long page loading time, also, let's implement SWR while we're at it...

In averages chart all data are accurate except for when I switch to

Amazing, let's move on to courses table and do the exact same thing

Actually, courses query are not that large only 138 courses, so let's keep it the same and only implement loading state

@courses-table.tsx

---

frontend issues
There's an issue when clicking on @order-form.tsx (426-439)

The request body is missing. @ServicesController.php (195-196)

Add "You are already enrolled here
similar to

backend issues
There's an issue when trying to create a new course @course-details.tsx (1230-1243)

{
"errors": {
"timings.0.start_time": "The timings.0.start_time field is required.",
"timings.2.start_time": "The timings.2.start_time field is required.",
"timings.3.start_time": "The timings.3.start_time field is required.",
"timings.4.start_time": "The timings.4.start_time field is required.",
"timings.0.end_time": "The timings.0.end_time field is required.",
"timings.1.end_time": "The timings.1.end_time field is required.",
"timings.3.end_time": "The timings.3.end_time field is required.",
"timings.4.end_time": "The timings.4.end_time field is required.",
"timings.0.capacity": "The timings.0.capacity field is required.",
"timings.1.capacity": "The timings.1.capacity field is required.",
"timings.2.capacity": "The timings.2.capacity field is required.",
"timings.4.capacity": "The timings.4.capacity field is required."
}
}

set tabby payment method as disabled "not allowed" if course/service total amount exceeds 8000SAR

sometimes when I click back in browser history I get raw data instead of actual page, why?
{"component":"courses\/course\/view\/index","props":{""}...}

then when I refresh I get the page normally!!!

when I do dd(...) in a controller, it takes 5-8 page reloads for it to take effect, why ?

proc_open is disabled causes issues with php queues in development and never starts manually as specified in entrypoint script...

✅ Caches cleared - Laravel will read .env dynamically

[14-Nov-2025 13:31:41] NOTICE: fpm is running, pid 5487

[14-Nov-2025 13:31:41] NOTICE: ready to handle connections

🚀 Starting queue listeners (with fresh config)...

⚠️ proc_open is disabled; starting processes individually...

INFO Processing jobs from the [etf-updates] queue.

Symfony\Component\Process\Exception\LogicException

The Process class relies on proc_open, which is not available on your PHP installation.

at vendor/symfony/process/Process.php:149
145▕ \*/
146▕ public function \_\_construct(array $command, ?string $cwd = null, ?array $env = null, mixed $input = null, ?float $timeout = 60)
147▕ {
148▕ if (!\function_exists('proc_open')) {
➜ 149▕ throw new LogicException('The Process class relies on proc_open, which is not available on your PHP installation.');
150▕ }
151▕
152▕ $this->commandline = $command;
153▕ $this->cwd = $cwd;

1 vendor/laravel/framework/src/Illuminate/Queue/Listener.php:122
Symfony\Component\Process\Process::\_\_construct("/app/apps/client")

2 vendor/laravel/framework/src/Illuminate/Queue/Listener.php:88
Illuminate\Queue\Listener::makeProcess("etf-updates", "etf-updates", Object(Illuminate\Queue\ListenerOptions))

3 vendor/laravel/framework/src/Illuminate/Queue/Console/ListenCommand.php:74
Illuminate\Queue\Listener::listen("etf-updates", "etf-updates", Object(Illuminate\Queue\ListenerOptions))

4 vendor/laravel/framework/src/Illuminate/Container/BoundMethod.php:36
Illuminate\Queue\Console\ListenCommand::handle()

5 vendor/laravel/framework/src/Illuminate/Container/Util.php:43
Illuminate\Container\BoundMethod::{closure:Illuminate\Container\BoundMethod::call():35}()

6 vendor/laravel/framework/src/Illuminate/Container/BoundMethod.php:96
Illuminate\Container\Util::unwrapIfClosure(Object(Closure))

7 vendor/laravel/framework/src/Illuminate/Container/BoundMethod.php:35
Illuminate\Container\BoundMethod::callBoundMethod(Object(Illuminate\Foundation\Application), Object(Closure))

8 vendor/laravel/framework/src/Illuminate/Container/Container.php:836
Illuminate\Container\BoundMethod::call(Object(Illuminate\Foundation\Application), [])

9 vendor/laravel/framework/src/Illuminate/Console/Command.php:211
Illuminate\Container\Container::call()

10 vendor/symfony/console/Command/Command.php:318
Illuminate\Console\Command::execute(Object(Symfony\Component\Console\Input\ArgvInput), Object(Illuminate\Console\OutputStyle))

11 vendor/laravel/framework/src/Illuminate/Console/Command.php:180
Symfony\Component\Console\Command\Command::run(Object(Symfony\Component\Console\Input\ArgvInput), Object(Illuminate\Console\OutputStyle))

12 vendor/symfony/console/Application.php:1073
Illuminate\Console\Command::run(Object(Symfony\Component\Console\Input\ArgvInput), Object(Symfony\Component\Console\Output\ConsoleOutput))

13 vendor/symfony/console/Application.php:356
Symfony\Component\Console\Application::doRunCommand(Object(Illuminate\Queue\Console\ListenCommand), Object(Symfony\Component\Console\Input\ArgvInput), Object(Symfony\Component\Console\Output\ConsoleOutput))

14 vendor/symfony/console/Application.php:195
Symfony\Component\Console\Application::doRun(Object(Symfony\Component\Console\Input\ArgvInput), Object(Symfony\Component\Console\Output\ConsoleOutput))

15 vendor/laravel/framework/src/Illuminate/Foundation/Console/Kernel.php:197
Symfony\Component\Console\Application::run(Object(Symfony\Component\Console\Input\ArgvInput), Object(Symfony\Component\Console\Output\ConsoleOutput))

16 vendor/laravel/framework/src/Illuminate/Foundation/Application.php:1235
Illuminate\Foundation\Console\Kernel::handle(Object(Symfony\Component\Console\Input\ArgvInput), Object(Symfony\Component\Console\Output\ConsoleOutput))

17 artisan:13
Illuminate\Foundation\Application::handleCommand(Object(Symfony\Component\Console\Input\ArgvInput))
