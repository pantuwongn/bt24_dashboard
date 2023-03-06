import ProjectTimeStatusColumn from "@/components/chart/column/project-time-status-column"
import { Select } from "antd"
import { FC } from "react"

interface IProps {
  className?: string
}

const TimeStatusList = [
  "Safety",
  "Internal loss",
  "De-carbon",
  "MH/MP saving"
]

const ProjectTimeStatusView: FC<IProps> = ({ className }) => {
  const parentClass = className ?? ''
  return (
    <div className={`flex flex-col justify-center items-center ${parentClass}`}>
      <Select className="w-full text-left" defaultValue={TimeStatusList[0]}>
        { TimeStatusList.map((timeStatus, index) => <Select.Option key={index}>{ timeStatus }</Select.Option>) }
      </Select>

      <ProjectTimeStatusColumn/>
    </div>
  )
}

export default ProjectTimeStatusView
