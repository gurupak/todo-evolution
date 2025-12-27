/**
 * Dashboard layout - pass through only
 * Header is rendered in page to avoid multiple useSession calls
 */
export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return children;
}
