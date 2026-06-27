import { Construction } from "lucide-react"
import { Button } from "@/components/ui/button"

export default function UnderConstruction() {
  return (
    <div className="fixed inset-0 flex items-center justify-center">
      <div className="flex flex-col items-center justify-center py-12 text-center">
        <h1 className="mb-4 text-2xl font-bold">Página en construcción</h1>
        <Construction className="h-20 w-20 text-amber-400" aria-hidden="true" />
        <p className="mt-3 mb-1 text-sm text-muted-foreground">
          Volver más tarde
        </p>
        <Button className="hover:cursor-pointer" onClick={() => {}}>
          Volver al inicio
        </Button>
      </div>
    </div>
  )
}
