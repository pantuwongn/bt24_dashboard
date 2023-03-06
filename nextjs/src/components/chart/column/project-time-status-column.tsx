import { FC } from "react"
import { ColumnConfig } from "@ant-design/charts"
import dynamic from "next/dynamic"

const Column = dynamic(() => import("@ant-design/charts").then((m) => m.Column), { ssr: false })

interface IProps { }

const data: Record<string, any>[] = [
  {
    name: 'Plan',
    plan: 'FY',
    actual: 104,
  },
  {
    name: 'Actual',
    plan: 'FY',
    actual: 86,
  },
]

const config: ColumnConfig = {
  data,
  isGroup: true,
  xField: 'plan',
  yField: 'actual',
  seriesField: 'name',
  color: ['#1ca9e6', '#f88c24'],
  marginRatio: 0.1,
  width: 180,
  height: 180,
  label: {
    position: 'middle',
    layout: [
      {
        type: 'interval-adjust-position',
      },
      {
        type: 'interval-hide-overlap',
      },
      {
        type: 'adjust-color',
      },
    ],
  },
}

const ProjectTimeStatusColumn: FC<IProps> = () => {
  return (
    <Column {...config} />
  )
}

export default ProjectTimeStatusColumn
