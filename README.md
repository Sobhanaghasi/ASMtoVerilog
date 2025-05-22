# ASMtoVerilog

A python script to translate ASM Charts into clean verilog code. The output would be written in ```asm.v``` and the input ASM chart should be represented in XML with the following conditions:


```<ASMChart>```: Root element with a chart name.

```<Variables>```: Lists registers; each ```<Variable>``` has:
```name```: variable name
```size```: bit width
optional ```type```: ```input``` or ```output```

```<StartState>```: The id of the starting ```<StateBox>```.
```<StateBox>```: Contains ```id```, ```<Name>```, multiple ```<Statement>```s (Verilog-syntax), and one ```<Destination>```.

```<DecisionBox>```": Contains id, a boolean ```<Condition>``` (Verilog-syntax), and two destinations:

```<TrueDestination>```: next box if condition is true

```<FalseDestination>```: next box if condition is false

```<ConditionBox>```: Contains ```id```, ```<Name>```, multiple ```<Statement>```s (Verilog-style), and one ```<Destination>```.

All destinations reference boxes by their id.



# Example:
```
<StartState>1</StartState>

<StateBoxes>
    <StateBox id="1">
        <Name>Init</Name>
        <Statements>
            <Statement>product &lt;= 0;</Statement>
            <Statement>count &lt;= 0;</Statement>
        </Statements>
        <Destination>10</Destination>
    </StateBox>

    <StateBox id="2">
        <Name>CheckDone</Name>
        <Destination>11</Destination>
    </StateBox>
</StateBoxes>

<DecisionBoxes>
    <DecisionBox id="10">
        <Condition>start == 0</Condition>
        <TrueDestination>1</TrueDestination>
        <FalseDestination>2</FalseDestination>
    </DecisionBox>

    <DecisionBox id="11">
        <Condition>count &lt; b</Condition>
        <TrueDestination>20</TrueDestination>
        <FalseDestination>12</FalseDestination>
    </DecisionBox>

    <DecisionBox id="12">
        <Condition>count == b</Condition>
        <TrueDestination>1</TrueDestination>
        <FalseDestination>2</FalseDestination>
    </DecisionBox>
</DecisionBoxes>

<ConditionBoxes>
    <ConditionBox id="20">
        <Name>AddAndIncrement</Name>
        <Statements>
            <Statement>product &lt;= product + a;</Statement>
            <Statement>count &lt;= count + 1;</Statement>
        </Statements>
        <Destination>12</Destination>
    </ConditionBox>
</ConditionBoxes>
```
