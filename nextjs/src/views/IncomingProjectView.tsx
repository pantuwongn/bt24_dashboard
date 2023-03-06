import { Tag } from "antd";
import { FC } from "react";
import { AiTwotoneFolder } from "react-icons/ai";

interface IProps {
  className?: string
}

const projectList = [
  "Add-on : Stator - Welding",
  "Add-on : Stator - Welding",
  "Add-on : Stator - Welding",
  "Add-on : Stator - Welding",
]

const IncomingProjectView: FC<IProps> = ({ className }) => {
  const parentClass = className ?? ''
  return (
    <div className={`grid grid-cols-4 gap-4 ${parentClass}`}>
      {projectList.map((project, index) =>
        <Tag key={index} icon={<AiTwotoneFolder className="mr-2"/>}>
          { project }
        </Tag>)}
    </div>
  )
}

export default IncomingProjectView
