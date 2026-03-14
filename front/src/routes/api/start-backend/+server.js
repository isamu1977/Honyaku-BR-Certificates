import { exec } from "child_process";
import { json } from "@sveltejs/kit";
import fkill from "fkill";

export async function POST({ request }) {
  try {
    const { action } = await request.json();
    const backendDir = "/Users/isamumatsuyama/Documents/development/honyaku-app/backend";
    
    if (action === "start") {
      const child = exec("uvicorn main:app --reload --host 0.0.0.0 --port 8080", {
          cwd: backendDir,
      });
      child.unref();
      return json({ success: true, message: "Backend started on port 8080" });
    } else if (action === "stop") {
      try {
        await fkill(':8080', { force: true, tree: true });
      } catch (e) {
        // Ignore errors if no process found
      }
      return json({ success: true, message: "Backend stopped" });
    } else {
      return json({ success: false, error: "Invalid action" }, { status: 400 });
    }
  } catch (error) {
    console.error("Failed to manage backend:", error);
    return json({ success: false, error: error.message }, { status: 500 });
  }
}
