import { Project } from "@/types/organization";

export function parseProjectStatusPieChart(project: Project, showComplete: boolean) {
  const data: Record<string, any>[] = [
    {
      type: 'Not start',
      value: project.num_not_start,
    },
    {
      type: 'Delay',
      value: project.num_delay,
    },
    {
      type: 'On plan',
      value: project.num_on_plan,
    }
  ]

  if (showComplete) {
    data.push({
      type: "Complete",
      value: project.num_completed
    })
  }
  return data
}

