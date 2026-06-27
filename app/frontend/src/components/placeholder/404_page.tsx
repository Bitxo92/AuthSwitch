import { Link } from "react-router-dom"

export function Page404() {
  return (
    <main className="relative flex min-h-screen items-center justify-center overflow-hidden bg-background px-6 py-12">
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_top,hsl(var(--primary)/0.18),transparent_58%)]" />

      <section className="relative z-10 w-full max-w-3xl text-center">
        <div className="relative mx-auto h-44 w-full sm:h-52">
          <div className="absolute inset-0 flex items-center justify-center">
            <span className="text-[4.2rem] leading-none font-black tracking-[-0.06em] text-foreground sm:text-[6rem]">
              404
            </span>
          </div>
        </div>

        <h1 className="mt-4 text-2xl font-semibold tracking-tight text-foreground sm:text-3xl">
          Error 404: Pagina no encontrada
        </h1>
        <p className="mx-auto mt-3 max-w-xl text-sm text-muted-foreground sm:text-base">
          La ruta que intentas abrir no existe o fue movida. Vuelve al inicio
          para continuar navegando.
        </p>

        <div className="mt-8 flex items-center justify-center">
          <Link
            to="/"
            className="inline-flex h-11 items-center justify-center rounded-md bg-primary px-6 text-sm font-medium text-primary-foreground transition-colors hover:bg-primary/90"
          >
            Volver al inicio
          </Link>
        </div>
      </section>
    </main>
  )
}
