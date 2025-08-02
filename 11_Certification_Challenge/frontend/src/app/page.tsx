import { CopilotKit } from "@copilotkit/react-core";
import "@copilotkit/react-ui/styles.css";
import { Mimi } from "./Components/Mimi";
export default function Home() {
  return (
    <>
      <CopilotKit showDevConsole runtimeUrl="api/copilotkit" agent="Mimi">
        <Mimi />
      </CopilotKit>
    </>
  );
}
