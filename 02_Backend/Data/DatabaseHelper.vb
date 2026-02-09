Imports System.Data.SQLite
Imports System.Configuration

Public Class DatabaseHelper
    Private ReadOnly ConnectionString As String
    
    Public Sub New()
        ConnectionString = ConfigurationManager.ConnectionStrings("TextileDB").ConnectionString
    End Sub
    
    Public Function GetConnection() As SQLiteConnection
        Dim connection As New SQLiteConnection(ConnectionString)
        connection.Open()
        Return connection
    End Function
    
    Public Function ExecuteNonQuery(sql As String, Optional parameters As Dictionary(Of String, Object) = Nothing) As Integer
        Using connection As SQLiteConnection = GetConnection()
            Using command As New SQLiteCommand(sql, connection)
                If parameters IsNot Nothing Then
                    For Each param In parameters
                        command.Parameters.AddWithValue(param.Key, param.Value)
                    Next
                End If
                
                Return command.ExecuteNonQuery()
            End Using
        End Using
    End Function
    
    Public Function ExecuteScalar(sql As String, Optional parameters As Dictionary(Of String, Object) = Nothing) As Object
        Using connection As SQLiteConnection = GetConnection()
            Using command As New SQLiteCommand(sql, connection)
                If parameters IsNot Nothing Then
                    For Each param In parameters
                        command.Parameters.AddWithValue(param.Key, param.Value)
                    Next
                End If
                
                Return command.ExecuteScalar()
            End Using
        End Using
    End Function
    
    Public Function GetDataTable(sql As String, Optional parameters As Dictionary(Of String, Object) = Nothing) As DataTable
        Using connection As SQLiteConnection = GetConnection()
            Using command As New SQLiteCommand(sql, connection)
                If parameters IsNot Nothing Then
                    For Each param In parameters
                        command.Parameters.AddWithValue(param.Key, param.Value)
                    Next
                End If
                
                Using adapter As New SQLiteDataAdapter(command)
                    Dim dt As New DataTable()
                    adapter.Fill(dt)
                    Return dt
                End Using
            End Using
        End Using
    End Function
End Class