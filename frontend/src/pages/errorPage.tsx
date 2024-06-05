import { useRouteError } from "react-router-dom";

export default function ErrorPage() {
    const error = useRouteError();
    console.error(error);

    return (
        <div className="flex flex-col gap-4 items-center w-full h-full justify-center">
            <h1 className=" text-8xl font-semibold">Oops!</h1>
            <p className=" text-lg">Sorry, an unexpected error has occurred.</p>
            <p className=" text-2xl">
                {/*@ts-ignore*/}
                <i>{error.statusText || error.message}</i>
            </p>
        </div>
    );
}