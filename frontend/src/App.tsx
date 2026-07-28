import { useEffect, useState } from "react";
import { ArchiveIcon } from "@phosphor-icons/react";
import { Button } from "./components/ui/Button";
import { Spoiler } from "./components/ui/Spoiler";
import {
  GoogleLogoIcon,
  UserIcon,
  FileIcon,
  DownloadIcon,
} from "@phosphor-icons/react";

// CountUp component for smooth counting effect
function CountUp({
  target,
  duration = 1800,
}: {
  target: number;
  duration?: number;
}) {
  const [count, setCount] = useState(0);

  useEffect(() => {
    let startTimestamp: number | null = null;
    let animationFrameId: number;

    const step = (timestamp: number) => {
      if (!startTimestamp) startTimestamp = timestamp;
      const progress = Math.min((timestamp - startTimestamp) / duration, 1);
      // Easing function for smooth count effect
      const easeOut = 1 - Math.pow(1 - progress, 3);
      setCount(Math.floor(easeOut * target));

      if (progress < 1) {
        animationFrameId = requestAnimationFrame(step);
      }
    };

    animationFrameId = requestAnimationFrame(step);
    return () => cancelAnimationFrame(animationFrameId);
  }, [target, duration]);

  return <>{count.toLocaleString()}</>;
}

function App() {
  return (
    <div className="flex h-screen w-full flex-col justify-between overflow-hidden bg-paper text-ink selection:bg-stamp/20">
      <header className="flex shrink-0 items-center justify-between px-4 sm:px-8 py-3.5 sm:py-5">
        <div className="flex items-center gap-2">
          <ArchiveIcon
            className="h-5 w-5 sm:h-6 sm:w-6 text-gray-800 shrink-0"
            weight="duotone"
          />
          <span className="font-serif text-lg sm:text-xl font-bold tracking-tight">
            tgstore
          </span>
        </div>
        <div className="flex items-center gap-2 sm:gap-3">
          <Button variant="ghost" size="sm" className="px-2.5 sm:px-5">
            Log in
          </Button>
          <Button size="sm" className="px-3 sm:px-5">
            Get started
          </Button>
        </div>
      </header>

      <main className="flex-1 flex flex-col items-center justify-center px-4 sm:px-8 pb-16 pt-2 text-center relative overflow-hidden">
        <div className="my-auto flex w-full max-w-5xl flex-col items-center justify-center gap-4 sm:gap-6 md:gap-8">
          <h1 className="font-serif text-[clamp(2.25rem,6.5vw,6.8rem)] leading-[1.03] tracking-tight font-normal text-ink px-2">
            Store Without <span className="font-bold">Limit</span>
          </h1>
          <p className="max-w-xs sm:max-w-md text-gray-950 text-[clamp(0.875rem,2vw,1.125rem)] leading-relaxed px-2">
            Limitless storage for each of your usecase{" "}
            <span className="block mt-1 sm:inline sm:mt-0">
              <Spoiler className="text-xs font-normal">
                (Hope Telegram don't hear us)
              </Spoiler>
            </span>
          </p>
          <div className="flex w-full sm:w-auto justify-center items-center px-4 mt-1">
            <Button
              size="md"
              className="w-full sm:w-auto max-w-xs sm:max-w-none gap-2.5 px-5 sm:px-8 py-3 text-sm sm:text-base md:text-lg shadow-sm hover:shadow transition-all"
            >
              <GoogleLogoIcon
                weight="bold"
                className="h-5 w-5 sm:h-6 sm:w-6 shrink-0"
              />
              <span className="truncate">Continue With Google</span>
            </Button>
          </div>
        </div>

        <div className="absolute bottom-3 sm:bottom-5 left-0 right-0 flex w-full justify-center items-center px-2">
          <div className="flex flex-wrap items-center justify-center gap-3 sm:gap-8 md:gap-10 text-[clamp(0.75rem,1.5vw,0.875rem)] text-ink/90">
            <p className="flex items-center gap-1.5 whitespace-nowrap">
              <span className="font-bold inline-flex items-center gap-1">
                <UserIcon
                  weight="duotone"
                  className="h-4 w-4 sm:h-5 sm:w-5 text-gray-800"
                />
                <CountUp target={1000} />
              </span>
              <span>Users</span>
            </p>

            <p className="flex items-center gap-1.5 whitespace-nowrap">
              <span className="font-bold inline-flex items-center gap-1">
                <FileIcon
                  weight="duotone"
                  className="h-4 w-4 sm:h-5 sm:w-5 text-gray-800"
                />
                <CountUp target={1000} />
              </span>
              <span>Files</span>
            </p>

            <p className="flex items-center gap-1.5 whitespace-nowrap">
              <span className="font-bold inline-flex items-center gap-1">
                <DownloadIcon
                  weight="duotone"
                  className="h-4 w-4 sm:h-5 sm:w-5 text-gray-800"
                />
                <CountUp target={1000} />
              </span>
              <span>Downloads</span>
            </p>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
