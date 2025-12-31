{{/*
Expand the name of the chart.
*/}}
{{- define "todo-app.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "todo-app.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "todo-app.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "todo-app.labels" -}}
helm.sh/chart: {{ include "todo-app.chart" . }}
{{ include "todo-app.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "todo-app.selectorLabels" -}}
app.kubernetes.io/name: {{ include "todo-app.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Frontend labels
*/}}
{{- define "todo-app.frontend.labels" -}}
{{ include "todo-app.labels" . }}
app.kubernetes.io/component: frontend
{{- end }}

{{/*
Backend labels
*/}}
{{- define "todo-app.backend.labels" -}}
{{ include "todo-app.labels" . }}
app.kubernetes.io/component: backend
{{- end }}

{{/*
MCP Server labels
*/}}
{{- define "todo-app.mcpServer.labels" -}}
{{ include "todo-app.labels" . }}
app.kubernetes.io/component: mcp-server
{{- end }}

{{/*
Frontend service account name
*/}}
{{- define "todo-app.frontend.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (printf "%s-frontend" (include "todo-app.fullname" .)) .Values.serviceAccount.frontend.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.frontend.name }}
{{- end }}
{{- end }}

{{/*
Backend service account name
*/}}
{{- define "todo-app.backend.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (printf "%s-backend" (include "todo-app.fullname" .)) .Values.serviceAccount.backend.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.backend.name }}
{{- end }}
{{- end }}

{{/*
MCP Server service account name
*/}}
{{- define "todo-app.mcpServer.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (printf "%s-mcp-server" (include "todo-app.fullname" .)) .Values.serviceAccount.mcpServer.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.mcpServer.name }}
{{- end }}
{{- end }}
