import { FC } from "react";
import { useForm } from "antd/lib/form/Form";
import { Button, Card, Form, Input } from "antd";
import { useRouter } from "next/router";

interface ILoginForm {
  username: string
  password: string
}

interface IProps { }
const LoginView: FC<IProps> = ({ }) => {
  const router = useRouter()
  const [form] = useForm<ILoginForm>()

  const handleFormSubmit = () => {
    router.push('/job-management')
  }

  return (
    <Card
      title="Login"
      style={{ width: 360 }}>
      <Form
        form={form}
        onFinish={handleFormSubmit}>
        <Form.Item name="username" label="Username">
          <Input />
        </Form.Item>
        <Form.Item name="password" label="Password">
          <Input type="password" />
        </Form.Item>

        <Form.Item>
          <div className="w-full flex justify-center">
            <Button key="login" type="primary" htmlType="submit">Login</Button>
          </div>
        </Form.Item>
      </Form>
    </Card>
  )
}

export default LoginView