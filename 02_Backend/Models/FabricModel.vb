' مدل پارچه در VB.NET
Public Class FabricModel
    Public Property FabricID As Integer
    Public Property FabricCode As String
    Public Property ProductID As Integer?
    Public Property Meterage As Decimal
    Public Property MachineNumber As String
    Public Property Weight As Decimal
    Public Property WarpWeave As String
    Public Property WeftWeave As String
    Public Property WarpNumber As String
    Public Property WeaverName As String
    Public Property DefectType As String
    Public Property ProductionDate As Date?
    Public Property ProductionTime As TimeSpan?
    Public Property CustomerID As Integer?
    Public Property InvoiceNumber As String
    Public Property InvoiceDate As Date?
    Public Property Status As String
    Public Property CreatedAt As Date?
    
    ' ویژگی‌های مرتبط
    Public Property ProductName As String
    Public Property CustomerName As String
End Class

Public Class FabricCreateModel
    Public Property FabricCode As String
    Public Property Meterage As Decimal
    Public Property MachineNumber As String
    Public Property Weight As Decimal
    Public Property WarpWeave As String
    Public Property WeftWeave As String
    Public Property WarpNumber As String
    Public Property WeaverName As String
    Public Property DefectType As String
    Public Property CustomerID As Integer?
    Public Property ProductID As Integer?
End Class